import { Dispatch, SetStateAction, useState } from "react";
import {
  Box,
  Button,
  CircularProgress,
  TextField,
  Typography,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";

import {
  ALLOWED_FILE_TYPES,
  API_ADDRESS,
  dataBankExamples,
} from "../../../../../config";

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
    const fileName = `${newValue}.pdb`;

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
            `https://mirna.cs.put.poznan.pl/api/query/structure/package?pdbid=${newValue}`
          );

          // if file exists
          if (res.status === 200) {
            const file = (await (
              await fetch(`http://files.rcsb.org/download/${fileName}`)
            ).blob()) as File;

            const formData = new FormData();
            formData.append("f", file, `${fileName}`);

            const resAPI = await fetch(`${API_ADDRESS}/get_models_and_chains`, {
              method: "POST",
              body: formData,
            });
            const json: { [key: string]: StructureModel } = await resAPI.json();
            const [model, chains] = Object.entries(json[fileName])[0];

            setFiles((old) =>
              old.concat({
                name: fileName,
                file,
                models: json[fileName],
                selectedModel: model,
                selectedChain: chains[0],
              })
            );
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
          columnGap: 1,
          rowGap: 2,
        }}
      >
        {dataBankExamples.map((example, i) => (
          <Button
            key={i}
            variant="contained"
            onClick={() => onInputChange(example.name, true)}
            disabled={
              inputState.loading ||
              ALLOWED_FILE_TYPES.some((type) =>
                uploadedFileNames.includes(`${example.name}.${type}`)
              )
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
