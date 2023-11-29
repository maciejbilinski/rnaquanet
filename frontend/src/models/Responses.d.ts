declare interface StateResponse {
  waiting: boolean;
  task_id?: string;
  task_url?: string;
  status?: number;
}

declare interface ResponseGetRmsd {
  task_id?: string;
}