declare interface IRequestRmsd {
  /** Is request currently being processed. */
  waiting: boolean;
  /** ID of the task (ex. "3gfg4TH"). */
  task_id?: string;
  /** URL of the task (ex. "http://site.net/3gfg4TH"). */
  task_url?: string;
  reqStatus?: ReqStatus;
}

declare interface ResponseRequestRmsd {
  task_id?: string;
}