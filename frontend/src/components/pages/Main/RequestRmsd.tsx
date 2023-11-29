import { Dispatch, SetStateAction, useState } from "react";
import { Box, Button, CircularProgress, Typography, useTheme } from "@mui/material";
import { Link } from "react-router-dom";

import { API_ADDRESS } from "../../../../config";

interface RequestRmsdProps {
  files: File[];
  setFiles: Dispatch<SetStateAction<File[]>>;
}

const RequestRmsd = ({ files, setFiles }: RequestRmsdProps) => {
  const [response, setResponse] = useState<IRequestRmsd>({
    waiting: false,
  });
  const theme = useTheme();

  const fetchData = async () => {
    try {
      setResponse({ waiting: true });

      // convert file array to FormData
      const formData = new FormData();
      files.forEach((file, i) => formData.append(`file_${i}`, file));

      const res = await fetch(`${API_ADDRESS}/request_rmsd`, {
        method: "POST",
        body: formData,
      });

      // if the API responded correctly, parse received data
      let json: ResponseRequestRmsd = {};
      if (res.status === 200) {
        json = await res.json();
        setFiles([]);
      }

      setResponse({
        waiting: false,
        task_id: json.task_id,
        task_url: json.task_id && `${location.origin}/${json.task_id}`,
        reqStatus: res.status,
      });
    }
    catch (error) {
      setResponse({
        waiting: false,
        reqStatus: 500,
      });
      console.error(error);
    }
  };

  const getMessage = () => {
    if (response.waiting) return <CircularProgress size="1.5rem" />;
    switch (response.reqStatus) {
      case 500:
        return "Server is not responding, please try again later";
      case 400:
        return "Uploaded files seem to be invalid, please try again";
      default:
        return "Upload files";
    }
  };

  return (
    <>
      <Button
        onClick={fetchData}
        variant="contained"
        disabled={!files.length || response.waiting}
      >
        {getMessage()}
      </Button>

      {(response.task_id) && (
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
          <Link to={response.task_id ?? ""}
            style={{
              color: theme.palette.primary.main,
            }}
          >
            {response.task_url}
          </Link>
        </Box>
      )}
    </>
  )
}

export default RequestRmsd