declare interface IRequestRmsd {
  /** Is request currently being processed. */
  waiting: boolean;
  reqStatus?: ReqStatus;
}

declare interface ResponseRequestRmsd {
  /** ID of the task (ex. "3gfg4TH"). */
  task_id?: string;
}

declare interface FileData {
  name: string;
  isFromDataBank: boolean;
  file?: File;
}
