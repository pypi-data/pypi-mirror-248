import os
import time
import pickle
import threading
import numpy as np
import faiss_apis.faiss_pb2
import faiss_apis.faiss_pb2_grpc
from collections import deque
from server.models import FaissIndexFlatIP


class SaveDataBase(threading.Thread):

    def __init__(self, func, interval, logger):
        threading.Thread.__init__(self)
        self._func = func
        self._interval = interval
        self._logger = logger
        self._dq = deque()

    def run(self):
        try:
            while True:
                if len(self._dq):
                    _status = self._dq.pop()
                    if _status:
                        self._func()
                time.sleep(self._interval)
        except Exception as e:
            self._logger.error("save-error:{}".format(e))

    @property
    def dp(self):
        return self._dq


class FaissServer(faiss_apis.faiss_pb2_grpc.FaissServiceServicer):

    def __init__(self, logger):
        self._db = {}
        self._logger = logger
        self._db_file = "faiss.db"
        self._db_path = "{}/faiss/".format(os.getcwd())
        self._db_file_path = "{}{}".format(self._db_path, self._db_file)
        self._load_db()
        self._sdb = SaveDataBase(self._save_db, 30, self._logger)
        self._sdb.start()

    def _load_db(self):
        if os.path.exists(self._db_file_path):
            with open(self._db_file_path, "rb") as f:
                self._db = pickle.load(f)
            self._logger.info("load db from {}".format(self._db_file_path))

    def _save_db(self):
        if not os.path.exists(self._db_path):
            os.mkdir(self._db_path)
        with open(self._db_file_path, "wb") as f:
            pickle.dump(self._db, f)
        self._logger.info("save db to {}".format(self._db_file_path))

    def Heartbeat(self, request, context):
        return faiss_apis.faiss_pb2.StatusResponse(
            status="200",
            message="server is alive!"
        )

    def LookIndexInfo(self, request, contex):
        dim, size = 0, 0
        if request.index_name in self._db:
            dim = self._db[request.index_name].dim
            size = len(self._db[request.index_name].ids)
        return faiss_apis.faiss_pb2.LookIndexResponse(
            index_name=request.index_name,
            dim=dim,
            size=size
        )

    def CreateIndex(self, request, context):
        status = "500"
        message = ""
        if request.type == "a":
            pass
        elif request.type == "b":
            pass
        else:
            if request.index_name not in self._db:
                self._db[request.index_name] = FaissIndexFlatIP(request.dim)
                self._save_db()
                status = "200"
                message = "index_name:{} is success create!".format(request.index_name)
            else:
                status = "300"
                message = "index_name:{} is existed!".format(request.index_name)
        return faiss_apis.faiss_pb2.StatusResponse(
            status=status,
            message=message
        )

    def DeleteIndex(self, request, contex):
        status = "500"
        if request.index_name in self._db:
            del self._db[request.index_name]
            status = "200"
        return faiss_apis.faiss_pb2.StatusResponse(
            status=status
        )

    def AddVector(self, request, context):
        status = "500"
        if request.index_name in self._db:
            faiss_index = self._db[request.index_name]
            if int(request.id) not in set(faiss_index.ids):
                inputs_vector = [val for val in request.vector.float_val]
                if len(inputs_vector) == faiss_index.dim:
                    faiss_index.ids.append(int(request.id))
                    faiss_index.index.add(np.array(inputs_vector).reshape(-1, faiss_index.dim))
                    self._sdb.dp.append(True)
                    status = "200"
                    message = "index_name:{} add vector is success!".format(request.index_name)
                else:
                    message = "inputs vector dim = {},  but index_name: {} dim = {}!".format(
                        len(inputs_vector), request.index_name, faiss_index.dim
                    )
            else:
                message = "vector id:{} is exist in index_name: {}".format(request.id, request.index_name)
        else:
            message = "index_name: {} is not exist, please create it!".format(request.index_name)
        return faiss_apis.faiss_pb2.StatusResponse(
            status=status,
            message=message
        )

    def Search(self, request, context):
        neighbors = []
        if request.index_name in self._db:
            faiss_index = self._db[request.index_name]
            inputs_vector = [val for val in request.vector.float_val]
            if len(inputs_vector) == faiss_index.dim:
                D, I = faiss_index.index.search(np.array(inputs_vector).reshape(-1, faiss_index.dim), request.top_k)
                for d, i in zip(D[0], I[0]):
                    neighbors.append({"id": faiss_index.ids[i], "score": d})
        return faiss_apis.faiss_pb2.SearchResponse(
            index_name=request.index_name,
            neighbors=neighbors
        )

    def SearchById(self, request, context):
        vector = []
        if request.index_name in self._db:
            faiss_index = self._db[request.index_name]
            vector = faiss_index.reconstruct(int(request.id)).tolist()
        return faiss_apis.faiss_pb2.SearchByIdResponse(
            index_name=request.index_name,
            vector=vector
        )
