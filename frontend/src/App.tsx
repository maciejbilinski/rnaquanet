import { useEffect, useMemo } from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { useLocalStorage } from "usehooks-ts";
import { Box } from "@mui/material";

import Navbar from "./components/Navbar";
import Main from "./components/Main";
import Footer from "./components/Footer";
import { BrowserRouter } from "react-router-dom";
import { projectName } from "../config";

function App() {
  const [colorMode, setColorMode] = useLocalStorage<"light" | "dark">("ColorMode", "dark");

  useEffect(() => {
    document.title = projectName;
  }, []);

  const theme = useMemo(() => (
    createTheme({
      palette: {
        mode: colorMode,
        background: {
          paper: colorMode === "light" ? "#ebebeb" : undefined
        },
        primary: {
          main: "#d26415",
        },
      },
      breakpoints: {
        values: {
          xs: 0,
          sm: 600,
          md: 900,
          lg: 1200,
          xl: 1536,
        },
      },
    })
  ), [colorMode]);

  return (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <Box sx={{
          display: "flex",
          justifyContent: "center",
          bgcolor: "background.default",
          color: "text.primary",
          height: "100vh",
          px: 2,
        }}>
          <Box sx={{
            display: "flex",
            flexDirection: "column",
            width: "100%",
            maxWidth: 900,
            gap: 1,
            my: 1,
          }}>
            <Navbar colorMode={colorMode} setColorMode={setColorMode} />
            <Main />
            <Footer />
          </Box>
        </Box>
      </ThemeProvider>
    </BrowserRouter>
  )
}

export default App
