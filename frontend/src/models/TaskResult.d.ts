declare interface ITaskResultRes {
  status?: ProcessingStatus;
  /** Recieved results if files were succesfully processed. */
  results?: Results;
  reqStatus?: ReqStatus;
}

declare interface TaskResultRes {
  status?: ProcessingStatus;
  results?: Results;
}

declare type Results = { [taskId: string]: Result };

declare interface Result {
  rmsd: number;
  error: number;
}
