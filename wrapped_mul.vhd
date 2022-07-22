library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity wrapped_mul is
	Port(
		din_a : in std_logic_vector        (7 downto 0);
		din_b : in std_logic_vector (7 downto 0);
		dout : out std_logic_vector (15 downto 0));
end wrapped_mul;
architecture struct of wrapped_mul is

component clock is
	Port ( clk : out STD_LOGIC);
end component;


component mul.vhd is
	Port(
		clk : in std_logic;
		din_a : in std_logic_vector        (7 downto 0);
		din_b : in std_logic_vector (7 downto 0);
		dout : out std_logic_vector (15 downto 0));
end component;

signal s_clk: std_logic;--signal s_clk is declared to offer acces on it from cocotb easily as dut.s_clk

begin
	clkpm: clock port map (clk => s_clk);

	toppm: mul.vhd port map(
		clk=> s_clk,
		din_a=> din_a,
		din_b=> din_b,
		dout=> dout);


end struct;