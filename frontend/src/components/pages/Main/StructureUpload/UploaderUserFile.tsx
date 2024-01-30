import { Dispatch, SetStateAction } from "react";
import { Box, Typography } from "@mui/material";

import FileUploaderList from "../../../fileUploader/FileUploaderList";
import FileUploader from "../../../fileUploader/FileUploader";

interface Props {
  files: FileData[];
  setFiles: Dispatch<SetStateAction<FileData[]>>;
}

const UploaderUserFile = ({ files, setFiles }: Props) => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 1,
      }}
    >
      <Typography>From local drive:</Typography>
      
      <Box
        sx={{
          display: "flex",
          flexDirection: { xs: "column", md: "row" },
          height: { xs: 300, md: 200 },
          gap: 2,
        }}
      >
        <FileUploader files={files} setFiles={setFiles} />
        <FileUploaderList files={files} setFiles={setFiles} />
      </Box>
    </Box>
  );
};

export default UploaderUserFile;
