import { Dispatch, SetStateAction, useState } from "react";
import { Box, Typography } from "@mui/material";
import { FileUploader as FileUploaderBase } from "react-drag-drop-files";
import UploadFileIcon from "@mui/icons-material/UploadFile";

import {
  MAX_UPLOAD_FILE_SIZE,
  MIN_UPLOAD_FILE_SIZE,
  ALLOWED_FILE_TYPES,
  API_ADDRESS,
} from "../../../config";

interface Props {
  files: FileData[];
  setFiles: Dispatch<SetStateAction<FileData[]>>;
}

const FileUploader = ({ files, setFiles }: Props) => {
  const [error, setError] = useState<"type" | "size" | null>(null);

  const handleChange = async (newFiles: FileList) => {
    const oldFileNames = files.map((d) => d.name);
    const newFilesArr = Array.from(newFiles);

    try {
      for (const file of newFilesArr) {
        let id = 2;
        // add a numeric suffix to the file name if it already exists
        if (oldFileNames.includes(file.name)) {
          const [fileName, fileExt] = file.name.split(".");
          let newFileName = "";
          do {
            newFileName = `${fileName} (${id++})${
              fileExt ? "." : ""
            }${fileExt}`;
          } while (oldFileNames.includes(newFileName));

          Object.defineProperty(file, "name", {
            writable: true,
            value: newFileName,
          });
        }
      }

      // request models and chains
      const formData = new FormData();
      newFilesArr.forEach((file, i) => {
        formData.append(`file_${i}`, file, file.name);
      });

      const res = await fetch(`${API_ADDRESS}/get_models_and_chains`, {
        method: "POST",
        body: formData,
      });
      const json: { [key: string]: StructureModel } = await res.json();

      setFiles((old) =>
        old.concat(
          newFilesArr.map((file) => {
            const [model, chains] = Object.entries(json[file.name])[0];

            return {
              name: file.name,
              file,
              models: json[file.name],
              selectedModel: model,
              selectedChain: chains[0],
            } as FileData;
          })
        )
      );
    } catch (error) {
      setError("type");
      console.error(error);
    }
  };

  return (
    <Box sx={{ flexBasis: "50%" }}>
      <FileUploaderBase
        handleChange={handleChange}
        types={ALLOWED_FILE_TYPES}
        dropMessageStyle={{
          opacity: 0.85,
        }}
        minSize={MIN_UPLOAD_FILE_SIZE}
        maxSize={MAX_UPLOAD_FILE_SIZE}
        onTypeError={() => setError("type")}
        onSizeError={() => setError("size")}
        onDrop={() => setError(null)}
        onSelect={() => setError(null)}
        children={
          <Box
            sx={(theme) => ({
              display: "flex",
              alignItems: "center",
              gap: 1,
              width: "100%",
              bgcolor: `${theme.palette[error ? "error" : "primary"].main}30`,
              border: "2px dashed",
              borderColor: theme.palette[error ? "error" : "primary"].main,
              borderRadius: 2,
              cursor: "pointer",
              px: 5,
              overflow: "hidden",
              "&:hover": {
                bgcolor: `${theme.palette[error ? "error" : "primary"].main}${
                  theme.palette.mode === "light" ? 45 : 20
                }`,
              },
            })}
          >
            <UploadFileIcon
              sx={{
                fontSize: 32,
                color: `${error ? "error" : "primary"}.main`,
              }}
            />
            <Box
              sx={{
                flexGrow: 1,
              }}
            >
              <Typography
                sx={{
                  fontSize: 12,
                  color: "text.secondary",
                }}
              >
                {error === "type" ? (
                  <span>Invalid file type!</span>
                ) : error === "size" ? (
                  <span>File too large!</span>
                ) : (
                  <span>
                    <u>Drop</u> your files here
                    <br />
                    or <u>click</u> to choose.
                  </span>
                )}
              </Typography>
            </Box>

            <Typography
              sx={{
                fontSize: 12,
                color: "text.secondary",
                maxWidth: 64,
              }}
            >
              {ALLOWED_FILE_TYPES.map((type) => `.${type}`).join(", ")}
            </Typography>
          </Box>
        }
        multiple
      />
    </Box>
  );
};

export default FileUploader;