import asyncio
import random
import re
import time
from cloudpss.utils.AsyncIterable import CustomAsyncIterable

from cloudpss.utils.httpAsyncRequest import graphql_fetch
from .view import getViewClass

from cloudpss.utils.IO import IO
from .messageStreamReceiver import MessageStreamReceiver

from cloudpss.utils.graphqlUtil import graphql_request
from .jobPolicy import JobPolicy
from .jobMachine import JobMachine
from .messageStreamSender import MessageStreamSender


class Job(object):
    """docstring for Job"""

    def __init__(
        self,
        id,
        args,
        createTime,
        startTime,
        endTime,
        status,
        context,
        user,
        priority,
        policy,
        machine,
        input,
        output,
        position,
    ):
        super(Job, self).__init__()
        self.id = id
        self.args = args
        self.createTime = createTime
        self.startTime = startTime
        self.endTime = endTime
        self.job_status = status #这里的status字段与原本的status()冲突
        self.context = context
        self.user = user
        self.priority = priority
        self.policy = policy  # type: ignore
        self.machine = JobMachine(**machine)  # type: ignore
        self.input = input
        self.output = output
        self.position = position
        self.__receiver = None
        self.__sender = None
        self._result = None

    @staticmethod
    async def fetch(id):
        """
        获取job信息
        """
        if id is None:
            raise Exception("id is None")
        query = """query($_a:JobInput!){
            job(input:$_a){
                id
                args
                createTime
                startTime
                endTime
                status
                context
                user
                priority
                policy  { 
                    name
                    queue
                    tres {
                        cpu
                        ecpu
                        mem
                    } 
                    priority 
                    maxDuration 
                }
                machine {
                    id
                    name
                    tres {
                        cpu
                        ecpu
                        mem
                    }
                }
                input
                output
                position
            }
        }"""
        variables = {"_a": {"id": id}}

        r = await graphql_fetch(query, variables)
        if "errors" in r:
            raise Exception(r["errors"])
        return Job(**r["data"]["job"])

    @staticmethod
    def fetchMany(*args):
        """
        批量获取任务信息
        """
        jobs = CustomAsyncIterable(Job.fetch,*args)
        return jobs
    

    @staticmethod
    async def create(revisionHash, job, config, name=None, rid="", policy=None, **kwargs):
        """
        创建一个运行任务

        :params: revision 项目版本号
        :params: job 调用仿真时使用的计算方案，为空时使用项目的第一个计算方案
        :params: config 调用仿真时使用的参数方案，为空时使用项目的第一个参数方案
        :params: name 任务名称，为空时使用项目的参数方案名称和计算方案名称
        :params: rid 项目rid，可为空

        :return: 返回一个运行实例

        >>> runner = Runner.runRevision(revision,job,config,'')
        """

        # 处理policy字段
        if policy is None:
            policy = {}
            if policy.get("tres", None) is None:
                policy["tres"] = {}
            policy["queue"] = job["args"].get("@queue", 1)
            policy["priority"] = job["args"].get("@priority", 0)
            tres = {"cpu": 1, "ecpu": 0, "mem": 0}
            tresStr = job["args"].get("@tres", "")
            for t in re.split("\s+", tresStr):
                if t == "":
                    continue
                k, v = t.split("=")
                tres[k] = float(v)  # type: ignore
            policy["tres"] = tres

        query = """mutation($input:CreateJobInput!){job:createJob(input:$input){id input output status position}}"""
        function = job["rid"].replace("job-definition/cloudpss/", "function/CloudPSS/")
        variables = {
            "input": {
                "args": {
                    **job["args"],
                    "_ModelRevision": revisionHash,
                    "_ModelArgs": config["args"],
                },
                "context": [
                    function,
                    rid,
                    f"model/@sdk/{str(int(time.time() * random.random()))}",
                ],
                "policy": policy,
            }
        }
        r = await graphql_fetch(query, variables)
        if "errors" in r:
            raise Exception(r["errors"])
        id = r["data"]["job"]["id"]
        return await Job.fetch(id)

    @staticmethod
    async def abort(id, timeout):
        """
        结束当前运行的算例

        """
        query = """mutation ($input: AbortJobInput!) {
            job: abortJob(input: $input) {
                id
                status
            }
        }
        """
        variables = {"input": {"id": id, "timeout": timeout}}
        await graphql_fetch(query, variables)

    @staticmethod
    def load(file, format="yaml"):
        return IO.load(file, format)

    @staticmethod
    def dump(job, file, format="yaml", compress="gzip"):
        return IO.dump(job, file, format, compress)

    async def read(self, receiver=None, dev=False, **kwargs):
        """
        使用接收器获取当前运行实例的输出
        """
        if receiver is not None:
            self.__sender = receiver
        if self.__receiver is None:
            self.__receiver = MessageStreamReceiver(self, dev)
        await self.__receiver.connect(**kwargs)
        return self.__receiver

    async def write(self, sender=None, dev=False, **kwargs) -> MessageStreamSender:
        """
        使用发送器为当前运行实例输入
        """

        if sender is not None:
            self.__sender = sender
        if self.__sender is None:
            self.__sender = MessageStreamSender(self, dev)
        await self.__sender.connect(**kwargs)
        return self.__sender
    
    def status(self):
        if self.__receiver is not None:
            return self.__receiver.status
        return 0

    @property
    def result(self):
        """
        获取当前运行实例的输出
        """
        if self._result is None:
            viewType = getViewClass(self.context[0])
            self._result = asyncio.run(self.view(viewType))
        return self._result

    async def view(self, viewType):
        """
        获取当前运行实例的输出
        """
        receiver = await self.read()
        sender = await self.write()
        return viewType(receiver, sender)
