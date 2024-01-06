import { Dispatch, SetStateAction } from "react";
import { Box, Button, Divider, Typography } from "@mui/material";

import FileUploaderList from "../../fileUploader/FileUploaderList";
import FileUploader from "../../fileUploader/FileUploader";

interface StructureSelectionProps {
  files: FileData[];
  setFiles: Dispatch<SetStateAction<FileData[]>>;
}

const StructureSelection = ({ files, setFiles }: StructureSelectionProps) => {
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
      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
        }}
      >
        <Button
          variant="outlined"
          onClick={async () => {
            const res = await fetch("http://files.rcsb.org/download/6rs3.pdb");
            console.log(res);
            console.log(await res.blob());
          }}
        >
          2HY9
        </Button>
        <Button>6RS3</Button>
      </Box>

      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 3,
          p: 1,
        }}
      >
        <Divider sx={{ flex: 1 }} />
        <Typography sx={{ fontSize: 14 }}>or / and</Typography>
        <Divider sx={{ flex: 1 }} />
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
