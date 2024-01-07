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
  const [response, setResponse] = useState<TaskRequest>();
  const [loading, setLoading] = useState<boolean>(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      // convert file array to FormData
      const formData = new FormData();

      files.forEach((fileData, i) => {
        if (fileData.file) {
          // files uploaded by user (send file with uniquefied file name)
          formData.append(`file_${i}`, fileData.file, fileData.name);
        } else {
          // files from protein data bank (send empty blob with file name as PDB id)
          formData.append(`file_${i}_pdb`, new Blob(), fileData.name);
        }
      });

      const res = await fetch(`${API_ADDRESS}/request_rmsd`, {
        method: "POST",
        body: formData,
      });

      // parse received data
      const json: TaskRequest = {
        status_code: res.status,
        ...(res.status === 200 ? await res.json() : {}),
      };

      // navigate to task url if `task_id` is returned
      if (json.task_id) {
        setFiles([]);
        navigate(`result/${json.task_id}`);
      }
      // else set the error message
      else {
        setResponse(json);
      }
    } catch (error) {
      setResponse({ status_code: 500 });
    }
    setLoading(false);
  };

  const getMessage = () => {
    if (loading) return <CircularProgress size="1.75rem" />;
    switch (response?.status_code) {
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
        disabled={!files.length || loading}
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
