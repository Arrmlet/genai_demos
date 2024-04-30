import os
from pathlib import Path


load_dotenv()


class Settings(BaseSettings):
    def __init__(self):
        super().__init__()
        self.init_paths()

    logging_level: str = 'INFO'
    logging_format: str = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

    service_addr: str = '0.0.0.0'
    service_port: int = 8000

    # Create a path for aggregation report csv file
    dataset_grid_dir: str = ''
    aggregation_data_dir: Path = Path(Path(os.getcwd()).parent)
    aggregation_data_dir: Path = aggregation_data_dir.joinpath(dataset_grid_dir)

    root_data_dir: str = ''
    question_filename: str = 'questions.json'
    document_dir_name: str = 'documents'
    grid_dir_name: str = 'grid'
    point_filename: str = 'point.json'

    # Whether to randomize the order of the given questions
    shuffle_questions: bool = False
    question_count: int = 1000

    # Ingest & ChromaDB Config
    chroma_db_impl: str = 'duckdb+parquet'  # Variable is no longer used in newer versions of chromadb
    target_source_chunks: int = 4
    embeddings_model_name: str = 'sentence-transformers/all-mpnet-base-v2'
    persist_directory: str = 'vector_db'
    vector_db: str = 'chroma'

    # Establish which prompt type to use in experiments
    prompt_template: str = 'llama_chat_prompt'  # 'hr_assistant_v1'

    # Establish which LLM to use in experiments
    llm_model: str = 'llama-7b-chat'  # 'bigscience_bloom-560m'
    huggingfacehub_api_token: None = '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'

    # PrivateGPT
    chunk_size: int = 500
    chunk_overlap: int = 50
    hide_source: bool = False
    mute_stream: bool = False

    question_file_path: Path | None = None
    document_dir_path: Path | None = None
    grid_dir_path: Path | None = None
    persist_dir_path: Path | None = None
    persist_dir_path_str: str | None = None
    chromadb_client_settings: ChromaDBSettings | None = None

    # Dataset s3 bucket
    s3_data_bucket_name: str = 'ness-genai-training-data'
    s3_data_dir_path: str = ''
    s3_dataset_key: str = 'dataset/'  # documents/
    s3_vdb_key: str = 'vector_db'
    # Result s3 bucket
    s3_results_bucket_name: str = ''
    s3_results_key: str = ''
    s3_questions_key: str = ''

    def init_paths(self):
        self.question_file_path = Path(self.root_data_dir, self.question_filename)  # 'data/HR_India/questions.json
        self.document_dir_path = Path(self.root_data_dir, self.document_dir_name)
        self.grid_dir_path = Path(self.root_data_dir, self.grid_dir_name)
        self.persist_dir_path = Path(self.root_data_dir, self.persist_directory)
        self.persist_dir_path_str = str(self.persist_dir_path)

        self.dataset_grid_dir = str(self.dataset_grid_dir)
        self.aggregation_data_dir: Path = Path(Path(os.getcwd()).parent)
        self.aggregation_data_dir: Path = self.aggregation_data_dir.joinpath(self.dataset_grid_dir)

        # Chroma
        self.chromadb_client_settings = ChromaDBSettings(
            # chroma_db_impl='duckdb+parquet',
            persist_directory=self.persist_dir_path_str,
            anonymized_telemetry=False,
            is_persistent=True
        )


settings = Settings()
