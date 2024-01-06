import { Dispatch, SetStateAction } from "react";
import { Box, Button, Card, Typography } from "@mui/material";
import { Link } from "react-router-dom";

import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { styles } from "../utils/styles";
import { projectName } from "../../config";

interface Props {
  colorMode: string;
  setColorMode: Dispatch<SetStateAction<"light" | "dark">>;
}

const Navbar = ({ colorMode, setColorMode }: Props) => {
  return (
    <Card
      sx={{
        ...styles.mainCard,
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        py: 2,
      }}
    >
      {/* filler box */}
      <Box
        sx={{
          flex: 1,
        }}
      />

      {/* project name */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Button variant="text">
          <Link
            to={location.origin}
            style={{
              color: "inherit",
              textDecoration: "none",
            }}
          >
            <Typography
              variant="h4"
              sx={{
                fontFamily: "initial",
              }}
            >
              {projectName}
            </Typography>
          </Link>
        </Button>
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
          onClick={() => setColorMode(colorMode === "dark" ? "light" : "dark")}
        >
          {colorMode === "dark" ? (
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
