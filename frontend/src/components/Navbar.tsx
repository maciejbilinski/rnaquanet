import { Dispatch, SetStateAction } from "react";
import { Box, Button, Card, Typography } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";

import { styles } from "../utils/styles";
import { projectName } from "../../config";

interface Props {
  colorMode: string;
  setColorMode: Dispatch<SetStateAction<"light" | "dark">>;
}

const Navbar = ({ colorMode, setColorMode }: Props) => {
  const navigate = useNavigate();

  return (
    <Card
      sx={{
        ...styles.mainCard,
        bgcolor: "primary.main",
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        py: 1,
      }}
    >
      {/* filler box */}
      <Box sx={{ flex: 1 }} />

      {/* project name */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Link
          to={window.origin}
          style={{
            textDecoration: "none",
            color: "inherit",
          }}
        >
          <Typography variant="h4" sx={{ fontFamily: "initial" }}>
            {projectName}
          </Typography>
        </Link>
      </Box>

      {/* theme toggle button */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          justifyContent: "flex-end",
        }}
      >
        <Button
          size="large"
          onClick={() => setColorMode(colorMode === "light" ? "dark" : "light")}
        >
          {colorMode === "light" ? (
            <Brightness7Icon color="action" />
          ) : (
            <Brightness4Icon color="action" />
          )}
        </Button>
      </Box>
    </Card>
  );
};

export default Navbar;
