export const steps = [
  {
    label: "Task uploaded",
    description: `Your task was uploaded to the server and will soon enter the queue
              or start processing if there are free resources.`,
  },
  {
    label: "Queued",
    description: `Our server is currently busy.
              Your task is currently waiting for resources in a queue.`,
  },
  {
    label: "Pending",
    description: `Your task is currently being processed.`,
  },
  {
    label: "Completed",
    description: ``,
  },
];

export const getCurrentStep = (response?: TaskResult): Step => {
  if (!response) return { id: 0, status: "loading" };
  switch (response.status_code) {
    case 500:
      return {
        id: 0,
        status: "failed",
        specialDescription: "Server is not responding, please try again later.",
      };
    case 404:
      return {
        id: 0,
        status: "failed",
        specialDescription:
          "The resources you are looking for can't be found. Check the URL that you were given.",
      };
    case 200:
      switch (response.status) {
        case "QUEUED":
          return { id: 1, status: "loading" };
        case "PENDING":
          return { id: 2, status: "loading" };
        case "DONE":
          return { id: 3, status: "success" };
        case "ERROR":
          return {
            id: 3,
            status: "failed",
            specialDescription:
              "There was an error when processing your files. This is most likely due to them being invalid.",
          };
        default:
          return {
            id: 3,
            status: "failed",
            specialDescription: "Unknown error.",
          };
      }
    default:
      return { id: 0, status: "loading" };
  }
};