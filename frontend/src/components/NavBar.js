import { AppBar, Button, Toolbar, Grid, Typography, Link } from "@mui/material";
import FlightTakeoffIcon from "@mui/icons-material/FlightTakeoff";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import { useState } from "react";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { useNavigate } from "react-router-dom";
import { Box } from "@mui/system";
import { useSelector } from "react-redux";

const NavBar = () => {
  // states to identify users
  const [passenger, setPassenger] = useState(false);
  const [airportAdmin, setAirportAdmin] = useState(false);
  const [airlineAdmin, setAirlineAdmin] = useState(false);

  // anchor for menu
  const [anchorEl, setAnchorEl] = useState(null);

  // state for menu
  const [menu, setMenu] = useState([
    {
      title: "Home",
      path: "/",
    },
    {
      title: "Reservation",
      path: "/reservation",
    },
    {
      title: "About",
      path: "/about",
    },
    {
      title: "Login",
      path: "/login",
    },
    {
      title: "Signup",
      path: "/signup",
    },
  ]);

  const navigate = useNavigate();
  const { isLoggedIn } = useSelector((state) => state.user);

  // functions to handle menu
  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleMenuClick = (path) => {
    setAnchorEl(null);
    navigate(path);
  };

  return (
    <nav>
      <AppBar>
        <Toolbar>
          <Grid
            container
            direction="row"
            alignItems="center"
            justifyContent="space-between"
          >
            <Grid item>
              <IconButton color="inherit" onClick={() => navigate("/")}>
                <FlightTakeoffIcon fontSize="large" />
              </IconButton>
            </Grid>

            <Grid item>
              <Box sx={{ display: { xs: "none", lg: "flex" } }}>
                <Typography variant="h2">YYC International Airport</Typography>
              </Box>
            </Grid>

            <Grid item>
              <Box sx={{ display: { xs: "flex", md: "none" } }}>
                <IconButton
                  size="large"
                  edge="start"
                  color="inherit"
                  aria-label="menu"
                  sx={{ mr: 2 }}
                  onClick={handleMenu}
                  aria-controls="menu-appbar"
                  aria-haspopup="true"
                >
                  <MenuIcon />
                </IconButton>
                <Menu
                  id="menu-appbar"
                  anchorEl={anchorEl}
                  anchorOrigin={{
                    vertical: "top",
                    horizontal: "right",
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: "top",
                    horizontal: "right",
                  }}
                  open={Boolean(anchorEl)}
                  onClose={() => setAnchorEl(null)}
                >
                  {menu.map((menu) => {
                    return (
                      <MenuItem
                        key={menu.title}
                        onClick={() => handleMenuClick(`${menu.path}`)}
                      >
                        {menu.title}
                      </MenuItem>
                    );
                  })}
                </Menu>
              </Box>
              {!isLoggedIn ? (
                <Box
                  sx={{ display: { xs: "none", md: "flex" }, width: "600px" }}
                  direction="row"
                  justifyContent="space-between"
                >
                  {menu.map((menu) => {
                    return (
                      <Button
                        variant="contained"
                        key={menu.title}
                        onClick={() => navigate(`${menu.path}`)}
                      >
                        {menu.title}
                      </Button>
                    );
                  })}
                </Box>
              ) : (
                <Box>LOGGED IN</Box>
              )}
            </Grid>
          </Grid>
        </Toolbar>
      </AppBar>
    </nav>
  );
};

export default NavBar;
