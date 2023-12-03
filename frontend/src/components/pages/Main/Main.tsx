import { useState } from "react";
import { Box, Card } from "@mui/material";

import { styles } from "../../../utils/styles";
import FileUpload from "./FileUpload";
import FileListDisplay from "./FileListDisplay";
import RequestRmsd from "./RequestRmsd";

const Main = () => {
  const [files, setFiles] = useState<File[]>([]);

  return (
    <Card sx={{
      ...styles.mainCard,
      py: 8,
      gap: 4,
    }}>
      <Box sx={{
        display: "flex",
        flexDirection: { xs: "column", md: "row" },
        height: { xs: 300, md: 200 },
        gap: 2,
      }}>
        <FileListDisplay files={files} setFiles={setFiles} />
        <FileUpload setFiles={setFiles} />
      </Box>

      <RequestRmsd files={files} setFiles={setFiles} />
    </Card>
  );
};

export default Main;