import { useState } from "react";
import { Box, Button, Card } from "@mui/material";

import { styles } from "../utils/styles";
import FileUpload from "./FileUpload";
import FileListDisplay from "./FileListDisplay";
import { API_ADDRESS } from "../../config";

const Main = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [awaitingResponse, setAwaitingResponse] = useState<boolean>(false);

  return (
    <Card sx={{
      ...styles.mainCard,
      py: 4,
      gap: 2,
    }}>
      <Box sx={{
        display: "flex",
        flexDirection: { xs: "column", md: "row" },
        height: { xs: 280, md: 140 },
        gap: 2,
      }}>
        <FileListDisplay files={files} setFiles={setFiles} />
        <FileUpload setFiles={setFiles} />
      </Box>

      <Button
        onClick={async () => {
          setAwaitingResponse(true);

          const formData = new FormData();
          files.forEach((file, i) => formData.append(`file_${i}`, file));

          console.log(formData.entries.length)

          const response = await fetch(`${API_ADDRESS}/get_rmsd`, {
            method: "POST",
            body: JSON.stringify({ files: formData }),
            headers: {
              "Content-Type": "application/json",
            },
          });

          const data = await response.json();
          console.log(data)

          setAwaitingResponse(false);
        }}
        variant="contained"
        disabled={!files.length}
      >
        Upload files
      </Button>
    </Card>
  );
};

export default Main;