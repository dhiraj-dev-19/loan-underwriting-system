import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#55624D',
      light: '#98A68E',
      dark: '#3E4A37',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#755754',
      light: '#FED7D2',
      dark: '#5B403D',
      contrastText: '#FFFFFF',
    },
    error: {
      main: '#BA1A1A',
      light: '#FFDAD6',
      dark: '#93000A',
    },
    background: {
      default: '#F8FAF3',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#1B1C1A',
      secondary: '#444841',
    },
    divider: '#E4E2DF',
  },
  typography: {
    fontFamily: "'Plus Jakarta Sans', sans-serif",
    h1: {
      fontFamily: "'Manrope', sans-serif",
      fontWeight: 700,
    },
    h2: {
      fontFamily: "'Manrope', sans-serif",
      fontWeight: 700,
    },
    h3: {
      fontFamily: "'Manrope', sans-serif",
      fontWeight: 600,
    },
    h4: {
      fontFamily: "'Manrope', sans-serif",
      fontWeight: 600,
    },
    h5: {
      fontFamily: "'Manrope', sans-serif",
      fontWeight: 600,
    },
    h6: {
      fontFamily: "'Manrope', sans-serif",
      fontWeight: 600,
    },
    subtitle1: {
      fontFamily: "'Plus Jakarta Sans', sans-serif",
      fontWeight: 600,
    },
    subtitle2: {
      fontFamily: "'Plus Jakarta Sans', sans-serif",
      fontWeight: 500,
    },
    body1: {
      fontFamily: "'Plus Jakarta Sans', sans-serif",
      fontWeight: 400,
      lineHeight: 1.6,
    },
    body2: {
      fontFamily: "'Plus Jakarta Sans', sans-serif",
      fontWeight: 400,
      lineHeight: 1.5,
    },
    button: {
      fontFamily: "'Plus Jakarta Sans', sans-serif",
      fontWeight: 600,
      textTransform: 'none',
    },
  },
  shape: {
    borderRadius: 24, // 24px rounded corners for main cards as requested
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '9999px', // Pill-shaped buttons
          padding: '10px 24px',
          fontWeight: 600,
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0 4px 14px rgba(85, 98, 77, 0.15)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 24,
          boxShadow: '0 4px 20px -2px rgba(85, 98, 77, 0.08)',
          border: 'none',
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          backgroundColor: '#F2F4ED',
          border: 'none',
          '& .MuiOutlinedInput-notchedOutline': {
            border: 'none',
          },
          '&.Mui-focused': {
            backgroundColor: '#FFFFFF',
            '& .MuiOutlinedInput-notchedOutline': {
              border: '2px solid #55624D',
            },
          },
        },
      },
    },
  },
});
