import { useState } from "react";
import {
  Card,
  Typography,
  Divider,
  Box,
  Checkbox,
  FormControlLabel,
} from "@mui/material";

import UploaderDataBank from "./UploaderDataBank";
import UploaderUserFile from "./UploaderUserFile";
import RequestButton from "./RequestButton";

import { styles } from "../../../../utils/styles";
import { useSessionStorage } from "usehooks-ts";

const StructureUpload = () => {
  const [files, setFiles] = useState<FileData[]>([]);
  const [isLocalAnalysis, setIsLocalAnalysis] = useSessionStorage<boolean>("isLocalAnalysis", false);

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
          justifyContent: "center",
          alignItems: "center"
        }}
      >
        <FormControlLabel
          sx={{ width: "fit-content", whiteSpace: "nowrap"}}
          label="Local analysis"
          control={
            <Checkbox
              checked={isLocalAnalysis}
              onChange={(props) => setIsLocalAnalysis(props.target.checked)}
            />
          }
        />

        <RequestButton
          files={files}
          setFiles={setFiles}
          isLocalAnalysis={isLocalAnalysis}
        />
      </Box>
    </Card>
  );
};

export default StructureUpload;
