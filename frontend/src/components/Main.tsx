import { Card } from "@mui/material";
import { FileUploader } from "react-drag-drop-files";

import { styles } from "../utils/styles";
import FileUpload from "./FileUpload";

const Main = () => {

  return (
    <Card sx={{
      ...styles.mainCard,
      alignItems: "center",
    }}>
      <FileUpload />
    </Card>
  );
};

export default Main;