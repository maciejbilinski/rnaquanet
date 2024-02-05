import { useState } from "react";
import {
  Card,
  Typography,
  Divider,
  Box,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  ListSubheader,
} from "@mui/material";

import UploaderDataBank from "./UploaderDataBank";
import UploaderUserFile from "./UploaderUserFile";
import RequestButton from "./RequestButton";

import { styles } from "../../../../utils/styles";
import { mlModels, defaultMlModel } from "../../../../../config";
import { useSessionStorage } from "usehooks-ts";

const StructureUpload = () => {
  const [files, setFiles] = useState<FileData[]>([]);
  const [mlModel, setMlModel] = useSessionStorage<MLModel>(
    "mlModel",
    defaultMlModel
  );

  return (
    <Card sx={styles.mainCard}>
      <Typography variant="h5" sx={{ textAlign: "center" }}>
        Upload 3D RNA structures
      </Typography>
      <UploaderDataBank files={files} setFiles={setFiles} />
      <Divider variant="middle" />
      <UploaderUserFile files={files} setFiles={setFiles} />
      <Divider variant="middle" />

      <Box
        sx={{
          display: "flex",
          flexDirection: { xs: "column", sm: "row" },
          gap: { xs: 0, sm: 1 },
        }}
      >
        <FormControl sx={{ width: "100%", maxWidth: { xs: "100%", sm: 250 } }}>
          <InputLabel>Computation model</InputLabel>
          <Select
            label="Computation model"
            value={mlModel.value}
            onChange={(e) => {
              const newM = mlModels.find((m) => m.value === e.target.value);
              if (newM) setMlModel(newM);
            }}
            renderValue={() => `${mlModel.name}  (${mlModel.type})`}
          >
            <ListSubheader color="primary">Global analysis</ListSubheader>
            {mlModels
              .filter((m) => m.type === "global")
              .map((m, i) => (
                <MenuItem
                  key={m.value}
                  value={m.value}
                  sx={{
                    p: 0,
                    width: "100%",
                    maxWidth: { xs: "100%", sm: 250 },
                    whiteSpace: "normal",
                  }}
                >
                  <div>
                    {i === 0 && <Divider />}
                    <Typography sx={{ p: 1 }}>
                      <i>{m.name}</i>
                      {` - ${m.description}`}
                    </Typography>
                    <Divider />
                  </div>
                </MenuItem>
              ))}
            <ListSubheader color="primary">Local analysis</ListSubheader>
            {mlModels
              .filter((m) => m.type === "local")
              .map((m, i) => (
                <MenuItem
                  key={m.value}
                  value={m.value}
                  sx={{
                    p: 0,
                    width: "100%",
                    maxWidth: { xs: "100%", sm: 250 },
                    whiteSpace: "normal",
                  }}
                >
                  <div>
                    {i === 0 && <Divider />}
                    <Typography sx={{ p: 1 }}>
                      <i>{m.name}</i>
                      {` - ${m.description}`}
                    </Typography>
                    <Divider />
                  </div>
                </MenuItem>
              ))}
          </Select>
        </FormControl>

        <RequestButton files={files} setFiles={setFiles} mlModel={mlModel} />
      </Box>
    </Card>
  );
};

export default StructureUpload;
