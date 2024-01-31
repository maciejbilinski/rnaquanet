/** Request status (200, 404, 500 etc). */
declare type ReqStatus = number;

/** Processing status of a single task. */
declare type TaskStatus = "QUEUED" | "PENDING" | "DONE" | "ERROR";

/** Processing status of a single file. */
declare type FileStatus = "WAITING" | "SUCCESS" | "ERROR";

/** Information about a single file. */
declare interface FileData {
  name: string;
  file?: File;
  models: StructureModel;
  selectedModel: string;
  selectedChain: string;
}

declare type StructureModel = { [key: string]: string[] };