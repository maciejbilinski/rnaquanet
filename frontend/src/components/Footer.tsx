import { Card, Link } from "@mui/material";

import { repositoryLink } from "../../config";
import { styles } from "../utils/styles";

const Footer = () => {
  return (
    <Card sx={{
      ...styles.mainCard,
      alignItems: "center",
      py: 2
    }}>
      <Link href={repositoryLink} target="_blank">
        Learn more about the project
      </Link>
    </Card>
  );
};

export default Footer;