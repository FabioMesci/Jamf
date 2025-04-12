-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-07-2023 a las 17:50:12
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `jamf`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes_pendientes`
--

CREATE TABLE `clientes_pendientes` (
  `ID_pedido` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `ID_pedido` int(11) NOT NULL,
  `cliente` varchar(255) NOT NULL,
  `producto` varchar(255) NOT NULL,
  `precio` double NOT NULL,
  `estado` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`ID_pedido`, `cliente`, `producto`, `precio`, `estado`) VALUES
(1, 'pedro', 'Capuchino', 3, ''),
(2, 'pedro', 'Café americano', 2, ''),
(3, 'pedro', 'Capuchino', 3, ''),
(4, 'pedro', 'Capuchino', 3, ''),
(5, 'pedro', 'Café americano', 2, ''),
(6, 'pedro', 'Capuchino', 3, ''),
(7, 'pedro', 'Capuchino', 3, ''),
(8, 'pedro', 'Latte', 3.5, ''),
(9, 'pedro', 'Capuchino', 3, ''),
(13, 'pedro', 'Capuchino', 3, ''),
(14, 'pedro', 'Capuchino', 3, ''),
(15, 'pedro', 'Latte', 3.5, ''),
(16, 'pedro', 'Latte', 3.5, ''),
(17, 'pedro', 'Café con leche', 2.5, ''),
(18, 'pedro', 'Capuchino', 3, ''),
(19, 'pedro', 'Capuchino', 3, ''),
(20, 'pedro', 'Café con leche', 2.5, ''),
(28, 'daniel', 'Capuchino', 3, ''),
(29, 'daniel', 'Capuchino', 3, ''),
(30, 'daniel', 'Café con leche', 2.5, ''),
(32, 'pedro', 'Café con leche', 2.5, ''),
(33, 'pedro', 'Café con leche', 2.5, ''),
(34, 'pedro', 'Doble espresso', 2.5, ''),
(36, 'daniel', 'Capuchino', 3, ''),
(37, 'daniel', 'Capuchino', 3, ''),
(38, 'daniel', 'Latte', 3.5, ''),
(40, 'daniel', 'Capuchino', 3, ''),
(41, 'daniel', 'Capuchino', 3, ''),
(42, 'daniel', 'Café con leche', 2.5, ''),
(44, 'Juan_Simón', 'Donut', 2.5, ''),
(45, 'Juan_Simón', 'Donut', 2.5, ''),
(46, 'Juan_Simón', 'Cortado', 3.5, ''),
(48, 'Juan_Simón', 'Donut', 2.5, ''),
(49, 'Juan_Simón', 'Cortado', 3.5, ''),
(50, 'Juan_Simón', 'Croissant', 3, ''),
(51, 'Juan_Simón', 'Café americano', 2, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos_cobrados`
--

CREATE TABLE `pedidos_cobrados` (
  `ID_pedido` int(11) NOT NULL,
  `cliente` varchar(255) NOT NULL,
  `pedido` varchar(255) NOT NULL,
  `precio` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `product_id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `precio` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`product_id`, `nombre`, `precio`) VALUES
(1, 'capuccino', 23412),
(2, 'Late', 2),
(6, 'cafe cortao', 2.5),
(7, 'asdasd', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `ci` int(11) NOT NULL,
  `password` varchar(255) NOT NULL,
  `PhoneNumber` int(12) NOT NULL,
  `Adress` text NOT NULL,
  `status` varchar(45) NOT NULL,
  `fecha_registro` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `email`, `username`, `ci`, `password`, `PhoneNumber`, `Adress`, `status`, `fecha_registro`) VALUES
(20, 'padron@gmail.com', 'admin', 29996624, '$2b$12$YYJxrET7QEH7Mp86OTqRV.Clv6Ztoj72Pi5JDaV9x1BYh1toDIyIm', 2147483647, 'admin123', 'admin', '2023-07-25'),
(36, 'Juan@gmail.com', 'jose', 29996624, '$2b$12$uLi7Klaz/eQfvyTGbFBSGek7HQPShf0RpS9hXI1R2EM2YZAo/Di3i', 2147483647, 'Av. Delicias, Sector Dr. Portillo', 'cocinero', '2023-07-03'),
(37, 'cliente@gmail.com', 'pedro', 29996624, '$2b$12$YLssgrIemIIitMyNugkfu.5XIONrdWHSXPAZ90PKfWmUcKSESedna', 2147483647, 'Av. Delicias, Sector Dr. Portillo', 'cliente', '2023-07-18'),
(38, 'padron@gmail.com', 'Juan', 29996624, '$2b$12$bz6YZyIH/Rp8MIdN5ci6Ze//MXSd6wIZ9ybIV/C6mDRrRyC4Bgf36', 2147483647, 'Av. Delicias, Sector Dr. Portillo', 'cliente', '2023-07-10'),
(39, 'padron@gmail.com', 'adminpro', 28752123, '$2b$12$OfIJxnM4w5nLBJ4zbrmoLO5.yfGgAV65P2lUYL1vV16AsM2G6fjyC', 2147483647, 'Av. Delicias, Sector Dr. Portillo', 'admin', '2023-07-10'),
(40, 'padron@gmail.com', 'daniel', 29996624, '$2b$12$rQ/PdkESIJjntYojSWKQzusI7Wb39BmaLNpFuPAOdMvWPRps3j98W', 2147483647, 'Av. Delicias, Sector Dr. Portillo', 'cliente', '2023-07-11'),
(43, 'juansiberdugo25@gmail.com', 'Juan_Pablo', 1534354, '$2b$12$TlqOo2f4VRC0xVUEqG9Ew.xZ8u3aL8.orhRJN8apK7P/Z98uuL80q', 1236812, 'por ahi en miami', 'empleado', '2023-07-26'),
(44, 'juansiberdugo25@gmail.com', 'Juan_Simón', 1213465, '$2b$12$TlqOo2f4VRC0xVUEqG9Ew.xZ8u3aL8.orhRJN8apK7P/Z98uuL80q', 1351524, 'por ahiii', 'cliente', '2023-07-26'),
(45, 'juansiberdugo25@gmail.com', 'Padre', 1213465, '$2b$12$MYmw8pQujn.DKmnjAbf1auDLMbJkSUSm3PYupEKSGO6V4bT/Q8v8a', 1236812, 'porahi', 'empleado', '2023-07-26'),
(46, 'juansiberdugo25@gmail.com', 'lulu', 665, '$2b$12$zGI187Y7i8QLu.ckGsloOukKPtsICCGP0OUz/V7jqqeqzGXUqyMOa', 96595, 'por hai', 'cocinero', '2023-07-26');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes_pendientes`
--
ALTER TABLE `clientes_pendientes`
  ADD PRIMARY KEY (`ID_pedido`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`ID_pedido`);

--
-- Indices de la tabla `pedidos_cobrados`
--
ALTER TABLE `pedidos_cobrados`
  ADD PRIMARY KEY (`ID_pedido`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`product_id`),
  ADD UNIQUE KEY `nombre` (`nombre`),
  ADD UNIQUE KEY `nombre_2` (`nombre`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes_pendientes`
--
ALTER TABLE `clientes_pendientes`
  MODIFY `ID_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `ID_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT de la tabla `pedidos_cobrados`
--
ALTER TABLE `pedidos_cobrados`
  MODIFY `ID_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1475;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
