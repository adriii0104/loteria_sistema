ALTER TABLE `lotteria_genuine`.`banca` 
DROP COLUMN `ganancias`,
ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST,
ADD COLUMN `persona_encargada` VARCHAR(45) NULL AFTER `bancacol`,
ADD COLUMN `numerocontacto` VARCHAR(45) NULL AFTER `persona_encargada`,
ADD COLUMN `contacto_secundario` VARCHAR(45) NULL AFTER `numerocontacto`,
ADD COLUMN `email_contacto` VARCHAR(45) NULL AFTER `contacto_secundario`,
ADD COLUMN `dia_pago` VARCHAR(45) NULL AFTER `email_contacto`,
ADD COLUMN `monto_pago` VARCHAR(45) NULL AFTER `dia_pago`,
ADD COLUMN `software_comprado` VARCHAR(45) NULL AFTER `monto_pago`,
ADD COLUMN `pago_punto` VARCHAR(45) NULL AFTER `software_comprado`,
ADD COLUMN `pago_pale` VARCHAR(45) NULL AFTER `pago_punto`,
ADD COLUMN `pago_tripleta` VARCHAR(45) NULL AFTER `pago_pale`,
CHANGE COLUMN `banca_auth` `nombre_banca` VARCHAR(45) NULL DEFAULT NULL ,
ADD PRIMARY KEY (`id`);
;





CREATE TABLE `lotteria_genuine`.`ganancias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_banca` VARCHAR(45) NULL,
  `tickets_vendidos` VARCHAR(45) NULL,
  `tickets_pagados` VARCHAR(45) NULL,
  `tickets_anulados` VARCHAR(45) NULL,
  `cantidad_pagada_diaria` VARCHAR(45) NULL,
  `cantidad_pagada_mensual` VARCHAR(45) NULL,
  `cantidad_pagada_anual` VARCHAR(45) NULL,
  `cantidad_pagada_total` VARCHAR(45) NULL,
  `venta_diaria` VARCHAR(45) NULL,
  `venta_mensual` VARCHAR(45) NULL,
  `venta_anual` VARCHAR(45) NULL,
  `venta_total` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));