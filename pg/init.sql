CREATE EXTENSION zhparser;
CREATE TEXT SEARCH CONFIGURATION chinese (PARSER = zhparser);
ALTER TEXT SEARCH CONFIGURATION chinese ADD MAPPING FOR n,v,a,i,e,l WITH simple;

CREATE TRIGGER vector_column_trigger
BEFORE INSERT OR UPDATE OF title, content, tsvector
ON ptt_post
FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger(
tsvector, 'public.chinese', title, content
);

UPDATE ptt_post SET tsvector = NULL;
