export const steps = [
  {
    label: "Finding the task",
    labelFinished: "Task submitted",
  },
  {
    label: "Uploading your task",
    labelFinished: "Task uploaded",
  },
  {
    label: "Queueing",
    labelFinished: "Queue finished",
  },
  {
    label: "Processing",
    labelFinished: "Processed",
  },
  {
    label: "Completion",
    labelFinished: "Completed",
  },
];

export const getCurrentStep = (
  lastStepId: number,
  response?: TaskResult
): Step => {
  if (!response) return { id: 0, status: "loading" };
  switch (response.status_code) {
    case 500:
      return {
        id: 0,
        status: "failed",
        specialDescription: "Server is not responding",
      };
    case 404:
      return {
        id: 0,
        status: "failed",
        specialDescription: "Task could not be found",
      };
    case 200:
      switch (response.status) {
        case "QUEUED":
          return { id: 2, status: "loading" };
        case "PENDING":
          return { id: 3, status: "loading" };
        case "DONE":
          return { id: 5, status: "success" };
        case "ERROR":
          return {
            id: 4,
            status: "failed",
            specialDescription: "Uploaded files were invalid",
          };
        default:
          return {
            id: 4,
            status: "failed",
            specialDescription: "An unknown error has occured.",
          };
      }
  }
  return {
    id: lastStepId,
    status: "failed",
    specialDescription: "An unknown error has occured.",
  };
};
