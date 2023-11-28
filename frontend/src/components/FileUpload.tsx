import { Dispatch, SetStateAction, useState } from "react";
import { Box, Typography } from "@mui/material";
import { FileUploader } from "react-drag-drop-files";
import UploadFileIcon from '@mui/icons-material/UploadFile';

import { MAX_UPLOAD_FILE_SIZE, MIN_UPLOAD_FILE_SIZE, UPLOAD_FILE_TYPES } from "../../config";

interface FileUploadProps {
  setFiles: Dispatch<SetStateAction<File[]>>;
}

const FileUpload = ({ setFiles }: FileUploadProps) => {
  const [error, setError] = useState<"type" | "size" | null>(null);

  return (
    <FileUploader
      handleChange={(newFiles: FileList) => (
        setFiles((old) => [
          ...old,
          ...Array.from(newFiles)
        ])
      )}
      types={UPLOAD_FILE_TYPES}
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
        <Box sx={(theme) => ({
          display: "flex",
          alignItems: "center",
          width: "100%",
          bgcolor: error ? "#ff000033" : undefined,
          border: "2px dashed",
          borderColor: theme.palette.primary.main,
          borderRadius: 2,
          cursor: "pointer",
          px: 2,
          gap: 1,
          overflow: "hidden",
        })}>
          <UploadFileIcon sx={(theme) => ({
            color: theme.palette.primary.main,
            fontSize: 32,
          })} />
          <Box sx={{
            flexGrow: 1
          }}>
            <Typography sx={{
              fontSize: 12,
              color: "#666",
            }}>
              {error === "type" ? (
                <span>Invalid file type!</span>
              ) : (error === "size") ? (
                <span>File too large!</span>
              ) : (
                <span>
                  <u>Drop</u> your files here<br />
                  or <u>click</u> to choose.
                </span>
              )}
            </Typography>
          </Box>

          <Typography sx={{
            fontSize: 12,
            color: "#666",
            maxWidth: 64,
          }}>
            {UPLOAD_FILE_TYPES.join(", ")}
          </Typography>
        </Box>
      }
      multiple
    />
  );
};

export default FileUpload;