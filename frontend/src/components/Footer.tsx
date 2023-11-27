import { Card, Link } from "@mui/material";

import { repositoryLink } from "../constants/creators";
import { styles } from "../utils/styles";

const Footer = () => {

  return (
    <Card sx={{
      ...styles.mainCard,
      alignItems: "center",
    }}>
      <Link href={repositoryLink} target="_blank">
        Source code
      </Link>
    </Card>
  );
};

export default Footer;