import { Dispatch, SetStateAction } from "react";
import { Box, Divider, Typography } from "@mui/material";

import FileUploaderList from "../../fileUploaders/FileUploaderList";
import FileUploader from "../../fileUploaders/FileUploader";
import DataBankUploader from "../../fileUploaders/DataBankUploader";

interface Props {
  files: FileData[];
  setFiles: Dispatch<SetStateAction<FileData[]>>;
}

const StructureSelection = ({ files, setFiles }: Props) => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 1,
      }}
    >
      <Typography variant="h5" sx={{ textAlign: "center" }}>
        Upload RNA structures
      </Typography>

      <Typography>From Protein Data Bank:</Typography>
      <DataBankUploader files={files} setFiles={setFiles} />

      <Box sx={{ p: 3 }}>
        <Divider />
      </Box>

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

export default StructureSelection;
