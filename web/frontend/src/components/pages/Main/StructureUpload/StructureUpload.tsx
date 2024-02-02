import { useState } from "react";
import {
  Card,
  Typography,
  Divider,
  TextField,
  Box,
  Autocomplete,
} from "@mui/material";

import UploaderDataBank from "./UploaderDataBank";
import UploaderUserFile from "./UploaderUserFile";
import RequestButton from "./RequestButton";

import { styles } from "../../../../utils/styles";
import { mlModels, defaultMlModel } from "../../../../../config";
import { useSessionStorage } from "usehooks-ts";

const StructureUpload = () => {
  const [files, setFiles] = useState<FileData[]>([]);
  const [mlModel, setMlModel] = useSessionStorage<MLModels>(
    "mlModel",
    defaultMlModel
  );

  return (
    <Card sx={styles.mainCard}>
      <Typography variant="h5" sx={{ textAlign: "center" }}>
        Upload RNA structures
      </Typography>
      <UploaderDataBank files={files} setFiles={setFiles} />
      <Divider variant="middle" />
      <UploaderUserFile files={files} setFiles={setFiles} />
      <Divider variant="middle" />

      <Box
        sx={{
          display: "flex",
          gap: 2,
        }}
      >
        <Autocomplete<MLModels, false, true>
          sx={{ width: "100%", maxWidth: 280 }}
          options={mlModels}
          value={mlModel}
          onChange={(_, newValue) => setMlModel(newValue)}
          getOptionLabel={(option) => `${option.name} - ${option.description}`}
          renderInput={(params) => (
            <TextField
              {...params}
              inputProps={{
                ...params.inputProps,
                value: mlModel.name,
              }}
              label="Computation model"
            />
          )}
          renderOption={(props, option) => (
            <div key={option.value}>
              <Divider />
              <li {...props}>
                <span>
                  <i>{option.name}</i>
                  {` - ${option.description}`}
                </span>
              </li>
            </div>
          )}
          disableClearable
        />

        <RequestButton files={files} setFiles={setFiles} mlModel={mlModel} />
      </Box>
    </Card>
  );
};

export default StructureUpload;
