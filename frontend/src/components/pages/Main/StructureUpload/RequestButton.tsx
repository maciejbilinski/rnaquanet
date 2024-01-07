import { Dispatch, SetStateAction, useState } from "react";
import { Button, CircularProgress } from "@mui/material";
import { useNavigate } from "react-router-dom";

import { API_ADDRESS } from "../../../../../config";

interface Props {
  files: FileData[];
  setFiles: Dispatch<SetStateAction<FileData[]>>;
}

const RequestButton = ({ files, setFiles }: Props) => {
  const navigate = useNavigate();
  const [response, setResponse] = useState<ITaskRequestRes>({
    waiting: false,
  });

  const fetchData = async () => {
    try {
      setResponse({ waiting: true });
      // convert file array to FormData
      const formData = new FormData();
      files.forEach((fileData, i) =>
        formData.append(`file_${i}`, fileData.file ?? new Blob(), fileData.name)
      );

      const res = await fetch(`${API_ADDRESS}/request_rmsd`, {
        method: "POST",
        body: formData,
      });

      // if the API responded correctly, parse received data
      let json: TaskRequestRes = {};
      if (res.status === 200) {
        json = await res.json();
        setFiles([]);
      }

      // navigate to task url when `task_id` is returned
      if (json.task_id) {
        navigate(`result/${json.task_id}`);
      }
      // else set the error message
      else {
        setResponse({
          waiting: false,
          reqStatus: res.status,
        });
      }
    } catch (error) {
      setResponse({
        waiting: false,
        reqStatus: 500,
      });
      console.error(error);
    }
  };

  const getMessage = () => {
    if (response.waiting) return <CircularProgress size="1.75rem" />;
    switch (response.reqStatus) {
      case 500:
        return "Server is not responding, please try again later";
      case 400:
        return "Uploaded files seem to be invalid, please try again";
      default:
        return "Submit task";
    }
  };

  return (
    <>
      <Button
        sx={{ height: 50 }}
        variant="contained"
        size="large"
        onClick={fetchData}
        disabled={!files.length || response.waiting}
      >
        {getMessage()}
      </Button>

      {/* {response.task_id && (
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Typography
            sx={{
              textAlign: "center",
            }}
          >
            Your files are being processed.
          </Typography>

          <Box>
            <Typography>Id of your task:</Typography>
            <Typography>{response.task_id}</Typography>
            <Typography></Typography>
            <Link
              to={response.task_id ? `result/${response.task_id}` : ""}
              style={{
                color: theme.palette.primary.main,
              }}
            >
              {response.task_url}
            </Link>
          </Box>
        </Box>
      )} */}
    </>
  );
};

export default RequestButton;
