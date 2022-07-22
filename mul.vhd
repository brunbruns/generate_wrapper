----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 03/30/2022 09:31:42 AM
-- Design Name: 
-- Module Name: mul - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity mul is
    Port ( clk :     in STD_LOGIC;
           din_a : in STD_LOGIC_VECTOR        (7 downto 0);
           
           
           din_b : in STD_LOGIC_VECTOR (7 downto 0);
           dout: out STD_LOGIC_VECTOR (15 downto 0));
end mul;



architecture Behavioral of mul is

signal s_a: signed (7 downto 0);
signal s_b: signed (7 downto 0);
signal s_out: signed (15 downto 0);

begin
process (clk)
    begin
    if rising_edge(clk) then
        s_out<=s_a*s_b;
    end if;
end process;

s_a<= signed(din_a);
s_b<=signed(din_b);
dout<=std_logic_vector(s_out);


end Behavioral;
