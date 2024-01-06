import { useState } from "react";
import { Card } from "@mui/material";

import { styles } from "../../../utils/styles";
import StructureSelection from "./StructureSelection";
import RequestButton from "./RequestButton";

const Main = () => {
  const [files, setFiles] = useState<FileData[]>([]);

  return (
    <Card
      sx={{
        ...styles.mainCard,
        py: 4,
        gap: 4,
      }}
    >
      <StructureSelection files={files} setFiles={setFiles} />
      <RequestButton files={files} setFiles={setFiles} />
    </Card>
  );
};

export default Main;