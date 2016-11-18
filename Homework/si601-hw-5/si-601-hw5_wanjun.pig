yelps = LOAD 'user/cteplovs/yelp_academic_dataset_review.json' USING JsonLoader('votes:map[], user_id:chararray, review_id:chararray, stars:int, date:chararray, text:chararray, type:chararray, business_id:chararray');
yelptext = FOREACH yelps GENERATE flatten(TOKENIZE(text)) AS word, stars;
positive = FILTER yelptext by stars >=5;
negative = FILTER yelptext by stars <=2;
positiveGroup = GROUP positive BY (word);
negativeGroup = GROUP negative BY (word);
all_review = GROUP yelptext BY (word);
positive2 = FOREACH positiveGroup GENERATE COUNT(positive) as countPositive, group;
negative2 = FOREACH negativeGroup GENERATE COUNT(negative) as countNegative, group;
all_reviews = FOREACH all_review GENERATE COUNT(yelptext) as countAll, group;
STORE all_reviews INTO 'output-step-1a';
STORE positive2 INTO 'output-step-1b';
STORE negative2 INTO 'output-step-1c';
all_reviews = FILTER all_reviews by countAll >= 1000;
positiveJoin = JOIN all_reviews by (group, countAll), positive2 by (group, countPositive);
negativeJoin = JOIN all_reviews by (group, countAll), negative2 by (group, countNegative);
STORE positiveJoin INTO 'output-step-2a';
STORE negativeJoin INTO 'output-step-2b';
positivity = LOAD 'output-step-2a' AS (word, countAll, word, CountPositive);
negativity = LOAD 'output-step-2b' AS (word, countAll, word, CountNegative);
Positivity(word) = log P(word in positivity) – log P(word in all_reviews); 
Negativity(word) = log P(word in negativity) - log P(word in all_reviews);
STORE Positivity(word) INTO 'output-positive';
STORE Negativity(word) INTO 'output-negative';






