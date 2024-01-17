import { Dispatch, SetStateAction, useState } from "react";
import { Box, Button, CircularProgress, TextField, Typography } from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";

import { dataBankExamples } from "../../../../../config";

interface Props {
  files: FileData[];
  setFiles: Dispatch<SetStateAction<FileData[]>>;
}

interface InputState {
  value: string;
  loading?: boolean;
  status?: "success" | "error";
}

const UploaderDataBank = ({ files, setFiles }: Props) => {
  const [inputState, setInputState] = useState<InputState>({ value: "" });
  const uploadedFileNames = files.map((file) => file.name);

  const onInputChange = async (newValue: string, skipPreview?: boolean) => {
    if (inputState.loading) return;
    newValue = newValue.toUpperCase();

    if (newValue.length === 4) {
      // if file with the same name is already added to file list
      if (files.map((file) => file.name).includes(newValue)) {
        setInputState({
          value: newValue,
          status: "error",
        });
      } else {
        // start loading and fetch data
        setInputState((old) => ({
          value: !skipPreview ? newValue : old.value,
          loading: true,
          status: undefined,
        }));
        try {
          const res = await fetch(
            `https://data.rcsb.org/rest/v1/core/entry/${newValue}`
          );
          // if file exists
          if (res.status === 200) {
            setFiles((old) =>
              old.concat({
                name: newValue,
                isFromDataBank: true,
              })
            );
            console.log(await res.json());
            setInputState((old) => ({
              value: !skipPreview ? "" : old.value,
              status: !skipPreview ? "success" : undefined,
            }));
          } else throw new Error();
        } catch {
          setInputState({
            value: newValue,
            status: "error",
          });
        }
      }
    } else if (newValue.length < 4) {
      if (inputState) setInputState({ value: newValue, loading: false });
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 1,
      }}
    >
      <Typography>From Protein Data Bank:</Typography>

      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
          gap: 1,
        }}
      >
        {dataBankExamples.map((example, i) => (
          <Button
            key={i}
            variant="contained"
            onClick={() => onInputChange(example.name, true)}
            disabled={
              inputState.loading || uploadedFileNames.includes(example.name)
            }
          >
            {example.name}
          </Button>
        ))}
        <TextField
          size="small"
          label="PDB id (e.g. 1FFK)"
          sx={{
            width: 200,
          }}
          value={inputState.value}
          onChange={(v) => onInputChange(v.target.value)}
          onBlur={() =>
            setInputState((old) => ({
              ...old,
              value: old.status === "error" ? "" : old.value,
              status: undefined,
            }))
          }
          InputProps={{
            spellCheck: false,
            endAdornment: inputState.loading ? (
              <CircularProgress size="1.5rem" />
            ) : inputState.status === "success" ? (
              <CheckCircleIcon color="success" />
            ) : inputState.status === "error" ? (
              <ErrorIcon color="error" />
            ) : (
              ""
            ),
          }}
          error={inputState.status === "error"}
        />
      </Box>
    </Box>
  );
};

export default UploaderDataBank;
