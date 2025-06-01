import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#1976d2" },
    background: { default: "#121212", paper: "#1e1e1e" },
  },
  typography: {
    fontFamily: "var(--font-geist-sans), var(--font-geist-mono), Roboto, Arial, sans-serif",
  },
});

export default theme; 
