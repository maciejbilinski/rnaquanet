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
    name: "2HY9",
  },
  {
    name: "6RS3",
  },
  {
    name: "1JJP",
  },
  {
    name: "6FC9",
  },
];


/** Name of the project. */
export const projectName = "RNAQuANet";

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