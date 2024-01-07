/** Request status (200, 404, 500 etc). */
declare type ReqStatus = number;

/** Processing status of a single task. */
declare type TaskStatus = "QUEUED" | "PENDING" | "DONE" | "ERROR";

/** Processing status of a single file. */
declare type FileStatus = "SUCCESS" | "ERROR";

/** Information about a single file. */
declare interface FileData {
  name: string;
  isFromDataBank: boolean;
  file?: File;
}