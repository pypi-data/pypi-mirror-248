#! python3.7


class Key:
    @classmethod
    def get_statistics_zset_key(cls, t: str, date: str):
        return f"alles-apin::{date}-{t}"

    @classmethod
    def get_last_statistics_job_date_key(cls):
        return f"alles-apin::last_statistics_job_update_date"

    @classmethod
    def get_api_health_key(cls, t: str):
        return f"alles-apin::api_wrong_time::{t}"

    @classmethod
    def get_openai_token_zset_key(cls, date: str):
        return f"alles-apin::openai_token::{date}"

