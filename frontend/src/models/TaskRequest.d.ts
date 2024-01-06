declare interface ITaskRequestRes {
  /** Is request currently being processed. */
  waiting: boolean;
  reqStatus?: ReqStatus;
}

declare interface TaskRequestRes {
  /** ID of the task (ex. "3gfg4TH"). */
  task_id?: string;
}

declare interface FileData {
  name: string;
  isFromDataBank: boolean;
  file?: File;
}
