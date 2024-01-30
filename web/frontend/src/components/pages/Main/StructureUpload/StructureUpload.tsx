import { useState } from 'react';
import { Card, Typography, Divider } from "@mui/material";

import UploaderDataBank from './UploaderDataBank';
import UploaderUserFile from './UploaderUserFile';
import RequestButton from "./RequestButton";

import { styles } from "../../../../utils/styles";

const StructureUpload = () => {
  const [files, setFiles] = useState<FileData[]>([]);
  
  return (
    <Card sx={styles.mainCard}>
      <Typography
        variant="h5"
        sx={{
          textAlign: "center",
        }}
      >
        Upload RNA structures
      </Typography>
      <UploaderDataBank files={files} setFiles={setFiles} />
      <Divider variant="middle" />
      <UploaderUserFile files={files} setFiles={setFiles} />
      <Divider variant="middle" />
      <RequestButton files={files} setFiles={setFiles} />
    </Card>
  );
};

export default StructureUpload