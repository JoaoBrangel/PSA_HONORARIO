
drop table if exists #TMP_NOME_ARQUIVOS_PSA
DECLARE @Diretorio				VARCHAR(100)		=	'\\192.168.4.46\cob_exportacao\PSA\'
DECLARE @DESTINO				VARCHAR(200)		=	'\\192.168.4.46\cob_exportacao\PSA\PROCESSADOS'
DECLARE @Nome_Arquivo			VARCHAR(100)		=	'*.csv'
DECLARE @MOVE					VARCHAR(255)
DECLARE @ARQUIVOESCOLHIDO		VARCHAR(200)

DECLARE @COMPLEMENTO_NOME		VARCHAR(255);
DECLARE @NOVO_NOME_ARQUIVO		VARCHAR(255);
DECLARE @Renomear				VARCHAR(500);
--######################################################################################################


CREATE TABLE #TMP_NOME_ARQUIVOS_PSA (N_ARQUIVO VARCHAR(500))
DECLARE @DIR					VARCHAR(100)		= 'DIR ' + @Diretorio + @Nome_Arquivo + '/B'

--######################################################################################################

INSERT INTO			#TMP_NOME_ARQUIVOS_PSA
EXEC xp_cmdshell	@DIR 
--select * from		#TMP_NOME_ARQUIVOS_PSA

SET @ARQUIVOESCOLHIDO = (
							SELECT 
									N_ARQUIVO 
							FROM	#TMP_NOME_ARQUIVOS_PSA	
							WHERE	N_ARQUIVO LIKE	'%.csv'
						)

--#######################################################################################################################


		SET @ARQUIVOESCOLHIDO = LEFT(@ARQUIVOESCOLHIDO, LEN(@ARQUIVOESCOLHIDO) - 4);

		SET @COMPLEMENTO_NOME = RIGHT('0'	+ CONVERT(VARCHAR(2), DATEPART(SECOND, GETDATE())), 2) + 
								RIGHT('000' + CONVERT(VARCHAR(4), DATEPART(MILLISECOND, GETDATE())), 3);

		SET @NOVO_NOME_ARQUIVO = @ARQUIVOESCOLHIDO + '_' + @COMPLEMENTO_NOME + '.csv';

		SET @Renomear = 'REN "' + @Diretorio + @ARQUIVOESCOLHIDO + '.csv" "' + @NOVO_NOME_ARQUIVO + '"';

		PRINT @Renomear;

		-- Executar o comando usando xp_cmdshell
		EXEC xp_cmdshell @Renomear;

--#######################################################################################################################

SET @MOVE = 'MOVE "' + @Diretorio + '\' + @NOVO_NOME_ARQUIVO + '" "' + @DESTINO + '\' + @NOVO_NOME_ARQUIVO + '"';

		EXEC xp_cmdshell @MOVE;	
