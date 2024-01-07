declare interface TaskRequest {
  /** Received status code. If there was an error, this will be the only available property. */
  status_code: number;
  /** ID of the task. */
  task_id?: string;
}

