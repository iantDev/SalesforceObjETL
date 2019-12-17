Create or Replace Function stg.proc_opportunity_update_from_stg() RETURNS void
AS $$

    INSERT into public.opportunity
    select s.*
    from stg.opportunity s
        LEFT join public.opportunity p on s.id = p.id
    where  s.systemmodstamp > p.systemmodstamp or s.id is not NULL


$$
LANGUAGE SQL