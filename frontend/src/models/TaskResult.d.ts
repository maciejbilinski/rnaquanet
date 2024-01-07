declare interface TaskResult {
  /** Received status code. If there was an error, this will be the only available property. */
  status_code: number;
  /** (`undefined` on error) Processing status of the whole task. */
  status?: TaskStatus;
  /** (`undefined` on error) Data of all files that are a part of the task. */
  files?: FileResult[];
}

declare interface FileResult {
  /** File id given by the db. */
  id: number;
  /** Is file temporary (removed from backend after processing). */
  is_temp: boolean;
  /** File name. */
  name: string;
  /** (`undefined` on error or if processing not complete) Calculated rmsd score. */
  rmsd?: number;
  /** Status of the file. */
  status: FileStatus;
  /** ID of the task. */
  task_id: string;
}
