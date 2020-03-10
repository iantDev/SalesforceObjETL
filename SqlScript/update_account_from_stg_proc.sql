
Create or Replace Function stg.proc_account_update_from_stg() RETURNS void
AS $$

    INSERT into public.account
    select s.*
    from stg.account s
        LEFT join public.account p on s.id = p.id
    where  s.systemmodstamp > p.systemmodstamp or s.id is not null;


$$
LANGUAGE SQL