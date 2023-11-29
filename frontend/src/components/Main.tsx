import { useState } from "react";
import { Box, Button, Card, Link, Typography } from "@mui/material";

import { styles } from "../utils/styles";
import FileUpload from "./FileUpload";
import FileListDisplay from "./FileListDisplay";
import { API_ADDRESS } from "../../config";

const Main = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [response, setResponse] = useState<StateResponse>({
    waiting: false,
  });

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
          setFiles([]);
          setResponse({ waiting: true });

          // convert file array to FormData
          const formData = new FormData();
          files.forEach((file, i) => formData.append(`file_${i}`, file));

          const res = await fetch(`${API_ADDRESS}get_rmsd`, {
            method: "POST",
            body: formData,
          });

          // if the API responded correctly, parse received data
          let json: ResponseGetRmsd = {};
          if (res.status === 200) {
            json = await res.json();
          }

          setResponse({
            waiting: true,
            task_id: json.task_id,
            task_url: json.task_id && `${window.location.origin}/${json.task_id}`,
            status: res.status,
          });
        }}
        variant="contained"
        disabled={!files.length}
      >
        Upload files
      </Button>

      {(response.task_url) && (
        <Box sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}>
          <Typography sx={{
            textAlign: "center",
          }}>
            Your files are being processed. Visit this link later to check the results.
          </Typography>
          <Link href={response.task_url}>
            {response.task_url}
          </Link>
        </Box>
      )}
    </Card>
  );
};

export default Main;