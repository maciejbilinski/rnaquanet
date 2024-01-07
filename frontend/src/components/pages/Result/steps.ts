export const steps = [
  {
    label: "Finding your task",
    labelFinished: "Task found",
    description: `We are trying to find your task in our database. It will take just a moment.`,
  },
  {
    label: "Uploading your task",
    labelFinished: "Task uploaded",
    description: `Your task was uploaded to the server and will soon enter the queue
              or start processing if there are free resources.`,
  },
  {
    label: "Queueing",
    labelFinished: "Queue finished",
    description: `Our servers are currently busy.
              Your task is currently waiting for resources in a queue.`,
  },
  {
    label: "Processing",
    labelFinished: "Processed",
    description: `Your task is currently being processed.`,
  },
  {
    label: "Completion",
    labelFinished: "Completion",
  },
];

export const getCurrentStep = (lastStepId: number, response?: TaskResult): Step => {
  if (!response) return { id: 0, status: "loading" };
  switch (response.status_code) {
    case 500:
      return {
        id: 0,
        status: "failed",
        specialDescription: [
          "Server is not responding.",
          "Please try again later.",
        ],
      };
    case 404:
      return {
        id: 0,
        status: "failed",
        specialDescription: [
          "The resources you are looking for can't be found.",
          "Check the URL that you were given.",
        ],
      };
    case 200:
      switch (response.status) {
        case "QUEUED":
          return { id: 2, status: "loading" };
        case "PENDING":
          return { id: 3, status: "loading" };
        case "DONE":
          return { id: 4, status: "success" };
        case "ERROR":
          return {
            id: 4,
            status: "failed",
            specialDescription: [
              "There was an error when processing your files.",
              "This is most likely due to them being invalid.",
              "Verify your files and try again.",
            ]
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
