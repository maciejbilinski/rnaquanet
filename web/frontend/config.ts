/** Minimal size of a file that user can upload (in MB). */
export const MIN_UPLOAD_FILE_SIZE = 0;

/** Maximal size of a file that user can upload (in MB). */
export const MAX_UPLOAD_FILE_SIZE = 20;

/** How long to wait between retrying to fetch results. (in ms). */
export const REQUEST_RETRY_DELAY = 5000;

/** List of available file types available for user to upload. */
export const ALLOWED_FILE_TYPES = ["pdb", "cif"];

/** URL to the API. */
export const API_ADDRESS = "http://localhost:5000";

// more constants

/** Example structures that will be displayed in the structure selector. */
export const dataBankExamples: DataBankExample[] = [
  {
    name: "1FFK",
  },
  {
    name: "7PS8",
  },
  {
    name: "7C7L",
  },
  {
    name: "6XLJ",
  },
];

/** Available machine learning models. */
export const mlModels: MLModel[] = [
  {
    value: "ares",
    name: "ARES",
    description: "model trained on ARES dataset",
  },
  {
    value: "seg1",
    name: "seg1",
    description: "model trained on only one segment descriptor",
  },
  {
    value: "seg2",
    name: "seg2",
    description: "model trained on only two segment descriptors",
  },
  {
    value: "seg3",
    name: "seg3",
    description: "model trained on only three and more segment descriptors",
  },
  {
    value: "transfer_seg2_ares",
    name: "transfer_seg2_ares",
    description: "model applies transfer learning on seg2 and ARES datasets",
  },
];

/** Which ML model should be selected by default. */
export const defaultMlModel: MLModel = mlModels[2];

/** Name of the project. */
export const projectName = "RNAQuANet";

export const pageTitle = `${projectName} | Quality assessment of 3D RNA structures`;

/** List of project creators. */
export const creators = [
  {
    name: "Bartek",
    lastName: "Adamczyk",
    github: "https://github.com/adamczykb",
  },
  {
    name: "Maciej",
    lastName: "Biliński",
    github: "https://github.com/maciejbilinski",
  },
  {
    name: "Mikołaj",
    lastName: "Bartkowiak",
    github: "https://github.com/Angelfrost",
  },
  {
    name: "Szymon",
    lastName: "Stanisławski",
    github: "https://github.com/Hi-Im-Simon",
  },
];

/** Link to the Github repository. */
export const repositoryLink = "https://github.com/maciejbilinski/rnaquanet";
