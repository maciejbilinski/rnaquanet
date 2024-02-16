declare interface TaskResult {
  /** Received status code. If there was an error, this will be the only available property. */
  status_code: number;
  /** Chosen type of analysis. */
  analysis_type?: AnalysisType;
  /** (`undefined` on error) Processing status of the whole task. */
  status?: TaskStatus;
  /** (`undefined` on error) Data of all files that are a part of the task. */
  files?: FileResult[];
}

declare interface FileResult {
  /** File id given by the db. */
  id: number;
  /** File name. */
  name: string;
  /** Structure's model selected by the user. */
  selectedModel: string;
  /** Structure's chain selected by the user. */
  selectedChain: string;
  /** (`undefined` on error or if processing not complete) Calculated rmsd score. */
  rmsd?: number;
  /** Status of the file. */
  status: FileStatus;
  /** ID of the task. */
  task_id: string;
  /** List of file descriptors. */
  descriptors?: Descriptor[];
}
